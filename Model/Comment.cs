using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class Comment : IModel {
        public int Id { get; set; }
        public string UserName { get; set; }
        public int AnswerId { get; set; }
        public int QuestionId { get; set; }
        public string Body { get; set; }
        public int Score { get; set; }
        public bool IsEdited { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }

        public Comment(SqlDataReader reader) {
            this.Id = int.Parse(reader["id"].ToString());
            this.UserName = reader["user_name"].ToString();
            this.AnswerId = (String.IsNullOrEmpty(reader["answer_id"].ToString())) ? 0 : int.Parse(reader["answer_id"].ToString());
            this.QuestionId = (String.IsNullOrEmpty(reader["question_id"].ToString())) ? 0 : int.Parse(reader["question_id"].ToString());
            this.Body = reader["body"].ToString();
            this.Score = int.Parse(reader["score"].ToString());
            this.IsEdited = bool.Parse(reader["edited"].ToString());
            this.CreationDate = ViewModel.strToDateTime(reader["creation_date"].ToString());
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
        }
    }
}
