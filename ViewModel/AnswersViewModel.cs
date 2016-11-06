using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class AnswersViewModel : ViewModel {

        public ObservableCollection<Answer> Answers { get; }

        public AnswersViewModel() {
            this.Answers = new ObservableCollection<Answer>();
        }

        protected override void createObject(SqlDataReader reader) {
            while(reader.Read()) {
                this.Answers.Add(new Answer(reader["id"].ToString(), reader["user_name"].ToString(), reader["question_id"].ToString(), reader["is_accepted"].ToString(), reader["body"].ToString(), reader["score"].ToString(), reader["up_vote_count"].ToString(), reader["creation_date"].ToString()));
            }
        }

        public void getAnswersByQId(int question_id) {
            string query = "SELECT answers.*, users.display_name AS user_name FROM answers JOIN users ON users.id = answers.user_id WHERE question_id=" + question_id;
            this.selectData(query);
        }
    }
}
