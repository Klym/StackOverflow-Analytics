delete from comments
delete from answers
delete from q_tags
delete from tags
delete from questions
delete from users
DBCC CHECKIDENT (tags, RESEED, 0)