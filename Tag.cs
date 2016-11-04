using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class Tag {
        public int Id { get; set; }
        public string Name { get; set; }
        public int Count { get; set; }
        public bool HasSynonyms { get; set; }

        public Tag(string id, string name, string count, string has_synomyms) {
            this.Id = int.Parse(id);
            this.Name = name;
            this.Count = int.Parse(count);
            this.HasSynonyms = bool.Parse(has_synomyms);
        }
    }
}
