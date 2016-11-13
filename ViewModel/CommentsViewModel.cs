using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class CommentsViewModel : ViewModel<Comment> {

        public void getByAnswerId(int answer_id) {
            string query = "SELECT comments.*, users.display_name AS user_name FROM comments JOIN users ON users.id = comments.user_id WHERE answer_id=" + answer_id;
            this.selectData(query);
        }
    }
}
