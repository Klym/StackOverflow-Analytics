using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class CommentsViewModel : ViewModel {

        public ObservableCollection<Comment> Comments { get; }

        public CommentsViewModel() {
            this.Comments = new ObservableCollection<Comment>();
        }

        protected override void createObject(SqlDataReader reader) {
            while (reader.Read()) {
                this.Comments.Add(new Comment(reader["id"].ToString(), reader["user_name"].ToString(), reader["answer_id"].ToString(), reader["question_id"].ToString(), reader["body"].ToString(), reader["score"].ToString(), reader["edited"].ToString(), reader["creation_date"].ToString()));
            }
        }

        public void getByAnswerId(int answer_id) {
            string query = "SELECT comments.*, users.display_name AS user_name FROM comments JOIN users ON users.id = comments.user_id WHERE answer_id=" + answer_id;
            this.selectData(query);
        }
    }
}
