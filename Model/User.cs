using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class User : IModel {
        public int Id { get; set; }
        public string Type { get; set; }
        public string Name { get; set; }
        public int Age { get; set; }
        public int Reputation { get; set; }
        public bool IsEmploye { get; set; }
        public string Location { get; set; }
        public int ViewCount { get; set; }
        public int QuestionCount { get; set; }
        public int AnswerCount { get; set; }
        public DateTime CreationDate { get; set; }

        public User(SqlDataReader reader) {
            this.Id = int.Parse(reader["id"].ToString());
            this.Type = reader["user_type"].ToString();
            this.Name = reader["display_name"].ToString();
            this.Age = (!String.IsNullOrEmpty(reader["age"].ToString())) ? int.Parse(reader["age"].ToString()) : 0;
            this.Reputation = int.Parse(reader["reputation"].ToString());
            this.IsEmploye = bool.Parse(reader["is_employe"].ToString());
            this.Location = reader["location"].ToString();
            this.ViewCount = int.Parse(reader["view_count"].ToString());
            this.QuestionCount = int.Parse(reader["question_count"].ToString());
            this.AnswerCount = int.Parse(reader["answer_count"].ToString());
            this.CreationDate = ViewModel<IModel>.strToDateTime(reader["creation_date"].ToString());
        }
    }
}
