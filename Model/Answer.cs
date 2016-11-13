using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class Answer : IModel {
        public int Id { get; set; }
        public string UserName { get; set; }
        public int QuestionId { get; set; }
        public bool IsAccepted { get; set; }
        public string Body { get; set; }
        public int Score { get; set; }
        public int UpVoteCount { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }
        public CommentsViewModel CommentsVM { get; set; }

        public Answer(SqlDataReader reader) {
            this.Id = int.Parse(reader["id"].ToString());
            this.UserName = reader["user_name"].ToString();
            this.QuestionId = int.Parse(reader["question_id"].ToString());
            this.IsAccepted = bool.Parse(reader["is_accepted"].ToString());
            this.Body = reader["body"].ToString();
            this.Score = int.Parse(reader["score"].ToString());
            this.UpVoteCount = int.Parse(reader["up_vote_count"].ToString());
            this.CreationDate = ViewModel<IModel>.strToDateTime(reader["creation_date"].ToString());
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
        }
    }
}