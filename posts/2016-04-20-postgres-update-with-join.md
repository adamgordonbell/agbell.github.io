---
title: Postgres Update With Join
author: Adam Bell
tags: postgres, cte, update
---

How to perform and update with a join using CTE's in postgres

* in a cte, write a select that returns the update to values, and the join on conditions
* join on that in the update
* Test: Optionally write a select that tests your results and wrap it all in a rolled back transaction to test run

<!--more-->
### Writing and testing the select as a cte

``` sql
with replacement as (
 select value, condtion1, condtion2 from somewhere
  where x= something
 )
 select * from replacement
```

*The cte might seem verbose, but I'm going to need it later, and it helps my sql stay organized*

### Testing the select as an update, without applying changes

``` sql
BEGIN;


with replacement as (
 select value, condtion1, condtion2 from somewhere
  where x= something
 )

 update "LongName" as shortname
 set value = replacement.value
 from replacement
 where shortname.condtion1 = replacement.condtion1
 and shortname.condtion2 = replacement.condition2;

-- Test query for manually confirming the results look like what you were expecting
SELECT value, condition1, condition2 from "LongName" shortname
where x=something

 ROLLBACK;

```

If the select result looks good, you can run it without the transaction to update.

### Run it

``` sql
with replacement as (
 select value, condtion1, condtion2 from somewhere
  where x= something
 )

 update "LongName" as shortname
 set value = replacement.value
 from replacement
 where shortname.condtion1 = replacement.condtion1
 and shortname.condtion2 = replacement.condition2;

```
