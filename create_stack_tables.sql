create table users (
	id				int primary key,
	user_type		varchar(14) not null,
	display_name	varchar(45) not null,
	age				smallint null check(age > 0),
	reputation		int not null check(reputation >= 0),
	is_employe		bit not null,
	creation_date	date not null,
	location		varchar(55) null,
	view_count		int not null check(view_count >= 0),
	question_count	int not null check(question_count >= 0),
	answer_count	int not null check(answer_count >= 0)
)

create table tags (
	id				int identity primary key,
	name			varchar(50) not null,
	count			int not null check(count >= 0),
	has_synonyms	bit not null
)

create table questions (
	id				int primary key,
	user_id			int not null foreign key references users(id),
	title			varchar(255) not null,
	body			text not null,
	is_answered		bit not null,
	view_count		int not null check(view_count >= 0),
	answer_count	int not null check(answer_count >= 0),
	score			int not null,
	up_vote_count	int not null check(up_vote_count >= 0),
	creation_date	date not null
)

create table q_tags (
	question_id		int not null foreign key references questions(id),
	tag_id			int not null foreign key references tags(id)
)

create table answers (
	id				int primary key,
	user_id			int not null foreign key references users(id),
	question_id		int not null foreign key references questions(id),
	is_accepted		bit not null,
	body			text not null,
	score			int not null,
	up_vote_count	int not null check(up_vote_count >= 0),
	creation_date	date not null
)

create table comments (
	id				int primary key,
	user_id			int not null foreign key references users(id),
	reply_to_user	int null foreign key references users(id),
	post_id			int not null,
	post_type		bit not null,
	body			text not null,
	score			int not null check(score >= 0),
	edited			bit not null,
	creation_date	date not null
)