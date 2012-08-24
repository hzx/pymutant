// pseudo-coded a bit, but embedded lunascript
// query that generates the task list UI is basically:

select concat(

  select from tasks where completed=true
    order by completion_time,

  select from tasks where completed=false
    order by priority

)
