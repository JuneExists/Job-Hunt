-- Job Hunt: shared usernames and reviews.
-- Paste this whole file into Supabase → SQL Editor → New query, then press Run. Safe to run more than once.

-- Usernames: one row per person. The database itself refuses a username that's already taken.
create table if not exists public.people (
  id uuid primary key references auth.users on delete cascade,
  username text not null unique check (username ~ '^[a-z0-9_.]{3,20}$'),
  login text not null unique,          -- the private sign-in id the app made for this person (not a real email)
  created_at timestamptz not null default now()
);

-- Reviews: one per person per company.
create table if not exists public.reviews (
  user_id uuid not null references auth.users on delete cascade,
  company_key text not null check (char_length(company_key) <= 120),
  company text not null check (char_length(company) <= 120),
  stars int not null check (stars between 1 and 5),
  text text not null default '' check (char_length(text) <= 600),
  role text not null default '' check (char_length(role) <= 120),
  status text not null default '' check (char_length(status) <= 30),
  at bigint not null,
  primary key (user_id, company_key)
);

alter table public.people enable row level security;
alter table public.reviews enable row level security;

-- Anyone can see usernames and reviews. People can only add or change their own.
drop policy if exists "people are public" on public.people;
create policy "people are public" on public.people for select using (true);
drop policy if exists "add my username" on public.people;
create policy "add my username" on public.people for insert with check (auth.uid() = id);
drop policy if exists "change my username" on public.people;
create policy "change my username" on public.people for update using (auth.uid() = id) with check (auth.uid() = id);

drop policy if exists "reviews are public" on public.reviews;
create policy "reviews are public" on public.reviews for select using (true);
drop policy if exists "write my reviews" on public.reviews;
create policy "write my reviews" on public.reviews for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
