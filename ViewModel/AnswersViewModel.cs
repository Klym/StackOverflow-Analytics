using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class AnswersViewModel : ViewModel<Answer> {

        public void getAnswersByQId(int question_id) {
            string query = "SELECT answers.*, users.display_name AS user_name FROM answers JOIN users ON users.id = answers.user_id WHERE question_id=" + question_id;
            this.selectData(query);
        }
    }
}
