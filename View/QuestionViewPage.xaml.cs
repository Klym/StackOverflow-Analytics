using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace StackOverflow_Analytics.View {
    /// <summary>
    /// Interaction logic for QuestionViewPage.xaml
    /// </summary>
    public partial class QuestionViewPage : Page {

        public Question Question { get; set; }

        public QuestionViewPage(Question question) {
            InitializeComponent();
            this.Question = question;
            this.Question.AnswersVM = new AnswersViewModel();
            this.Question.AnswersVM.getAnswersByQId(this.Question.Id);
            for (int i = 0; i < this.Question.AnswersVM.Answers.Count; i++) {
                this.Question.AnswersVM.Answers[i].CommentsVM = new CommentsViewModel();
                this.Question.AnswersVM.Answers[i].CommentsVM.getByAnswerId(this.Question.AnswersVM.Answers[i].Id);
            }
            DataContext = this.Question;
        }
    }
}
