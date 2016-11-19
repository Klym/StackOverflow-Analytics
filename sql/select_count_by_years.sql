select Count(questions.id) as cnt, datepart(yyyy, questions.creation_date) as year 
from q_tags 
join tags on tag_id = id 
join questions on questions.id = question_id 
where name='c#' 
group by datepart(yyyy, questions.[creation_date])
order by year