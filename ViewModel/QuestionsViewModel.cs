using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;
using System.Data;

namespace StackOverflow_Analytics {
    public class QuestionsViewModel : ViewModel<Question> {

        public QuestionsViewModel() {
            // Достаем вопросы для которых есть ответы и комментарии
            string query = "select TOP 100 questions.*, users.display_name AS u_name FROM questions JOIN users ON user_id = users.id WHERE (select COUNT(id) from comments WHERE answer_id in (select id from answers where question_id = questions.id)) > 0 ORDER BY score DESC";
            this.selectData(query);
        }
    }
}