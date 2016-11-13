using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class UsersViewModel : ViewModel<User> {

        public UsersViewModel() {
            string query = "SELECT TOP 300 * FROM users ORDER BY reputation DESC";
            this.selectData(query);
        }
    }
}
