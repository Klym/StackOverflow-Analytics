using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class Comment {
        public int Id { get; set; }
        public string UserName { get; set; }
        public int AnswerId { get; set; }
        public int QuestionId { get; set; }
        public string Body { get; set; }
        public int Score { get; set; }
        public bool IsEdited { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }

        public Comment(string id, string userName, string answerId, string questionId, string body, string score, string isEdited, string creationDate) {
            this.Id = int.Parse(id);
            this.UserName = userName;
            this.AnswerId = (String.IsNullOrEmpty(answerId)) ? 0 : int.Parse(answerId);
            this.QuestionId = (String.IsNullOrEmpty(questionId)) ? 0 : int.Parse(questionId);
            this.Body = body;
            this.IsEdited = bool.Parse(isEdited);
            string[] parseDate = creationDate.Split('.');
            this.CreationDate = new DateTime(int.Parse(parseDate[2].Substring(0, parseDate[2].IndexOf(' '))), int.Parse(parseDate[1]), int.Parse(parseDate[0]));
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
        }
    }
}
