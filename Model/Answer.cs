using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackOverflow_Analytics {
    public class Answer {
        public int Id { get; set; }
        public string UserName { get; set; }
        public int QuestionId { get; set; }
        public bool IsAccepted { get; set; }
        public string Body { get; set; }
        public int Score { get; set; }
        public int UpVoteCount { get; set; }
        public DateTime CreationDate { get; set; }
        public string DateString { get; set; }
        public CommentsViewModel CommentsVM { get; set; }

        public Answer(string id, string userName, string questionId, string isAccepted, string body, string score, string upVoteCount, string creationDate) {
            this.Id = int.Parse(id);
            this.UserName = userName;
            this.QuestionId = int.Parse(questionId);
            this.IsAccepted = bool.Parse(isAccepted);
            this.Body = body;
            this.Score = int.Parse(score);
            this.UpVoteCount = int.Parse(upVoteCount);
            string[] parseDate = creationDate.Split('.');
            this.CreationDate = new DateTime(int.Parse(parseDate[2].Substring(0, parseDate[2].IndexOf(' '))), int.Parse(parseDate[1]), int.Parse(parseDate[0]));
            this.DateString = this.CreationDate.ToString("dd.MM.yyyy");
        }
    }
}