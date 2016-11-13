using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class Question : IModel {
        public int Id { get; set; }
        public string UserName { get; set; }
        public string Title { get; set; }
        public string Body { get; set; }
        public bool IsAnswered { get; set; }
        public int AnswerCount { get; set; }
        public int ViewCount { get; set; }
        public int Score { get; set; }
        public int UpVoteCount { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }
        public TagsViewModel TagsVM { get; set; }
        public AnswersViewModel AnswersVM { get; set; }

        public Question(SqlDataReader reader) {
            this.Id = int.Parse(reader["id"].ToString());
            this.UserName = reader["u_name"].ToString();
            this.Title = reader["title"].ToString();
            this.Body = reader["body"].ToString();
            this.IsAnswered = bool.Parse(reader["is_answered"].ToString());
            this.AnswerCount = int.Parse(reader["answer_count"].ToString());
            this.ViewCount = int.Parse(reader["view_count"].ToString());
            this.Score = int.Parse(reader["score"].ToString());
            this.UpVoteCount = int.Parse(reader["up_vote_count"].ToString());
            this.CreationDate = ViewModel<IModel>.strToDateTime(reader["creation_date"].ToString());
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
        }
    }
}
