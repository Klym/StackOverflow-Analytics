using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data.SqlClient;

namespace StackOverflow_Analytics {
    public class Tag : IModel {
        public int Id { get; set; }
        public string Name { get; set; }
        public int Count { get; set; }
        public bool HasSynonyms { get; set; }
        public string Description { get; set; }

        public Tag(SqlDataReader reader) {
            this.Id = int.Parse(reader["id"].ToString());
            this.Name = reader["name"].ToString();
            this.Count = int.Parse(reader["count"].ToString());
            this.HasSynonyms = bool.Parse(reader["has_synonyms"].ToString());
            this.Description = reader["description"].ToString();
        }
    }
}
