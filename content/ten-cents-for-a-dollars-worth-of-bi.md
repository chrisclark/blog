Title: A Dollars Worth of BI for Ten Cents
Date: 2016-10-27
Status: Draft
Author: Chris
Slug: a-dollars-worth-of-bi-for-ten-cents
Category: Data Science

How to get a mid-market data warehouse, for an entry-level price.

You have a problem. You have data in 3 or 4 relational databases, but want join and report across all of them, in one place, in SQL. If you are a Fortune 1000 insurance company, I have good news; this problem has a very well-established solution: Pay Informatica $15 million to integrate everything into a badass data warehouse.

If you're a series A company, however, your board of directors may frown ominously and mutter things about 'fiduciary duty' when you get to that slide in the board deck. You might need something a bit more economical. Here's what we did at Grove.

Grove is growing. We're an ecommerce company and our primary datastore is our primary, transactional ecommerce database but increasingly have important data in other sources; marketing data from our email and analytics systems, purchasing and vendor data from warehousing and operational systems, and a handful of other small services floating around in EC2. We rely heavily on SQL (actual, like, SQL code as well as BI GUI tools that are powered by SQL under the covers) for reporting, but our data is isolated in separate DBs. At best, this is totally annoying because you have to join things up in Excel (or worse), and at worst it means a lot of data questions go unanswered because it's too much of a pain in the neck.

We faced a second challenge as well -- our engineering team was reaching the point where we were no longer comfortable reporting directly out of our production ecommerce database. Some of our tables are getting large, and a beefy query can start to impact, materially, CPU load on our production DB instance.

We needed a true analytics data warehouse. But I didn't want to pay for one.

-- FIRST, as RDS superuser -- Do this once on the production DB.
CREATE EXTENSION postgres_fdw;
GRANT ALL ON FOREIGN DATA WRAPPER postgres_fdw to application_user;


-- THEN as application_user

CREATE SERVER segment
 FOREIGN DATA WRAPPER postgres_fdw
 OPTIONS (host '<host>', dbname '<dbname>', port '5432');

CREATE USER MAPPING FOR application_user SERVER segment OPTIONS (user '<foreign_server_username>', password '<foreign_server_password>');

-- You can do this via:
-- pg_dump -h ec2-23-21-164-237.compute-1.amazonaws.com -p 5432 -U guasdesgdkvoyy -t purchase_orders --schema-only d8bsv6fmmqgf7v

CREATE FOREIGN TABLE segment_tracks (
    id character varying(1024) NOT NULL,
    received_at timestamp with time zone,
    uuid_ts timestamp with time zone,
    anonymous_id text,
    context_campaign_content text,
    context_campaign_medium text,
    context_campaign_name text,
    context_campaign_source text,
    context_integration_name text,
    context_integration_version text,
    context_ip text,
    context_library_name text,
    context_library_version text,
    context_page_path text,
    context_page_referrer text,
    context_page_search text,
    context_page_title text,
    context_page_url text,
    context_traits_email text,
    context_user_agent text,
    event text,
    event_text text,
    original_timestamp timestamp with time zone,
    sent_at timestamp with time zone,
    "timestamp" timestamp with time zone,
    user_id text
) SERVER segment OPTIONS (schema_name 'segment', table_name 'tracks');
