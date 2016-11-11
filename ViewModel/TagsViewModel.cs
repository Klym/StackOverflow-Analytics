using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class TagsViewModel : ViewModel {

        protected override IModel createObject(SqlDataReader reader) {
            return new Tag(reader);
        }

        public void getTagsModelByQId(int question_id) {
            string query = "SELECT * FROM q_tags JOIN tags ON id = tag_id WHERE question_id=" + question_id;
            this.selectData(query);
        }
    }
}
