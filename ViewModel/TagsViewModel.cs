using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class TagsViewModel : ViewModel {

        public ObservableCollection<Tag> Tags { get; }

        public TagsViewModel() {
            this.Tags = new ObservableCollection<Tag>();
        }

        protected override void createObject(SqlDataReader reader) {
            while (reader.Read()) {
                this.Tags.Add(new Tag(reader["id"].ToString(), reader["name"].ToString(), reader["count"].ToString(), reader["has_synonyms"].ToString()));
            }
        }

        public void getTagsModelByQId(int question_id) {
            string query = "SELECT * FROM q_tags JOIN tags ON id = tag_id WHERE question_id=" + question_id;
            this.selectData(query);
        }
    }
}
