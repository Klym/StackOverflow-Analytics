using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
using System.Data;

namespace StackOverflow_Analytics {
    public class QuestionsViewModel : ViewModel {

        public ObservableCollection<Question> Questions { get; }

        public QuestionsViewModel() {
            string query = "SELECT TOP 300 questions.*, users.display_name AS u_name FROM questions JOIN users ON user_id = users.id ORDER BY score DESC";
            this.Questions = new ObservableCollection<Question>();
            this.selectData(query);
        }

        protected override void createObject(SqlDataReader reader) {
            while (reader.Read()) {
                Question question = new Question(reader["id"].ToString(), reader["u_name"].ToString(), reader["title"].ToString(), reader["body"].ToString(), reader["is_answered"].ToString(), reader["answer_count"].ToString(), reader["view_count"].ToString(), reader["score"].ToString(), reader["up_vote_count"].ToString(), reader["creation_date"].ToString());
                question.TagsVM = new TagsViewModel();
                question.TagsVM.getTagsModelByQId(question.Id);
                this.Questions.Add(question);
            }
        }
    }
}