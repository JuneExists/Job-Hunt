-- Job Hunt, part 2: review reports + moderation, password recovery codes, private sync, "hiring now" spots.
-- Run after supabase-setup.sql. Safe to run more than once.
create extension if not exists pgcrypto with schema extensions;

-- ---------- Moderation ----------
create table if not exists public.admins (user_id uuid primary key references auth.users on delete cascade);
create table if not exists public.app_secrets (name text primary key, value_hash text not null);
alter table public.admins enable row level security;
alter table public.app_secrets enable row level security;   -- no policies: nobody can read it through the API
drop policy if exists "admins are visible" on public.admins;
create policy "admins are visible" on public.admins for select using (true);

create or replace function public.is_admin() returns boolean language sql stable security definer set search_path = public as
$$ select exists(select 1 from public.admins where user_id = auth.uid()) $$;

-- The app owner enters a private code once to become an admin.
create or replace function public.claim_admin(p_code text) returns boolean language plpgsql security definer set search_path = public, extensions as $$
declare h text;
begin
  if auth.uid() is null then return false; end if;
  select value_hash into h from public.app_secrets where name = 'owner_code';
  if h is null or extensions.crypt(upper(trim(p_code)), h) <> h then return false; end if;
  insert into public.admins(user_id) values (auth.uid()) on conflict do nothing;
  return true;
end $$;

create table if not exists public.reports (
  reporter uuid not null references auth.users on delete cascade default auth.uid(),
  review_user uuid not null,
  company_key text not null,
  reason text not null check (char_length(reason) <= 200),
  at timestamptz not null default now(),
  primary key (reporter, review_user, company_key)
);
create table if not exists public.hidden_reviews (
  review_user uuid not null,
  company_key text not null,
  at timestamptz not null default now(),
  primary key (review_user, company_key)
);
alter table public.reports enable row level security;
alter table public.hidden_reviews enable row level security;
drop policy if exists "report a review" on public.reports;
create policy "report a review" on public.reports for insert with check (auth.uid() = reporter);
drop policy if exists "admins see reports" on public.reports;
create policy "admins see reports" on public.reports for select using (public.is_admin());
drop policy if exists "admins clear reports" on public.reports;
create policy "admins clear reports" on public.reports for delete using (public.is_admin());
drop policy if exists "hidden list is public" on public.hidden_reviews;
create policy "hidden list is public" on public.hidden_reviews for select using (true);
drop policy if exists "admins hide reviews" on public.hidden_reviews;
create policy "admins hide reviews" on public.hidden_reviews for all using (public.is_admin()) with check (public.is_admin());

-- ---------- Password recovery codes ----------
create table if not exists public.recovery (
  user_id uuid primary key references auth.users on delete cascade,
  code_hash text not null,
  tries int not null default 0,
  updated_at timestamptz not null default now()
);
alter table public.recovery enable row level security;   -- no policies: only the two functions below can touch it

create or replace function public.set_recovery(p_code text) returns boolean language plpgsql security definer set search_path = public, extensions as $$
begin
  if auth.uid() is null or char_length(p_code) < 12 then return false; end if;
  insert into public.recovery(user_id, code_hash, tries, updated_at) values (auth.uid(), extensions.crypt(upper(p_code), extensions.gen_salt('bf')), 0, now())
  on conflict (user_id) do update set code_hash = excluded.code_hash, tries = 0, updated_at = now();
  return true;
end $$;

-- Resets a password with the username + recovery code. Locks after 10 wrong tries.
create or replace function public.reset_password(p_username text, p_code text, p_new text) returns text language plpgsql security definer set search_path = public, extensions, auth as $$
declare uid uuid; r record;
begin
  if char_length(coalesce(p_new, '')) < 6 then return 'short'; end if;
  select id into uid from public.people where username = lower(trim(p_username));
  if uid is null then return 'nouser'; end if;
  select * into r from public.recovery where user_id = uid;
  if r is null then return 'nocode'; end if;
  if r.tries >= 10 then return 'locked'; end if;
  if extensions.crypt(upper(trim(p_code)), r.code_hash) <> r.code_hash then
    update public.recovery set tries = tries + 1 where user_id = uid; return 'badcode';
  end if;
  update auth.users set encrypted_password = extensions.crypt(p_new, extensions.gen_salt('bf')), updated_at = now() where id = uid;
  update public.recovery set tries = 0 where user_id = uid;
  return 'ok';
end $$;

-- ---------- Private sync (your profile + saved jobs, only you can see them) ----------
create table if not exists public.vault (
  user_id uuid primary key references auth.users on delete cascade default auth.uid(),
  profile jsonb not null default '{}'::jsonb,
  jobs jsonb not null default '[]'::jsonb,
  updated_at bigint not null default 0
);
alter table public.vault enable row level security;
drop policy if exists "my vault" on public.vault;
create policy "my vault" on public.vault for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ---------- "Hiring now" spots ----------
create table if not exists public.hiring_spots (
  user_id uuid not null references auth.users on delete cascade default auth.uid(),
  spot_key text not null check (char_length(spot_key) <= 200),
  company text not null check (char_length(company) <= 120),
  place text not null default '' check (char_length(place) <= 80),
  at timestamptz not null default now(),
  primary key (user_id, spot_key)
);
alter table public.hiring_spots enable row level security;
drop policy if exists "spots are public" on public.hiring_spots;
create policy "spots are public" on public.hiring_spots for select using (true);
drop policy if exists "add my spots" on public.hiring_spots;
create policy "add my spots" on public.hiring_spots for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
drop policy if exists "admins remove spots" on public.hiring_spots;
create policy "admins remove spots" on public.hiring_spots for delete using (public.is_admin());

-- ---------- Access for the app ----------
grant select on public.admins, public.hidden_reviews, public.hiring_spots to anon, authenticated;
grant insert, select, delete on public.reports to authenticated;
grant insert, update, delete on public.hidden_reviews to authenticated;
grant insert, update, delete on public.hiring_spots to authenticated;
grant select, insert, update, delete on public.vault to authenticated;
grant execute on function public.is_admin() to anon, authenticated;
grant execute on function public.claim_admin(text) to authenticated;
grant execute on function public.set_recovery(text) to authenticated;
grant execute on function public.reset_password(text, text, text) to anon, authenticated;
revoke all on public.app_secrets, public.recovery from anon, authenticated;
