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

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for TagsListPage.xaml
    /// </summary>
    public partial class TagsListPage : Page {

        private MainWindow mainWindow;

        public TagsListPage(TagsViewModel tagsViewModel) {
            InitializeComponent();
            DataContext = tagsViewModel;
        }

        private void Page_Loaded(object sender, RoutedEventArgs e) {
            this.mainWindow = (MainWindow)Window.GetWindow(this);
        }

        private void ListBoxItem_MouseDoubleClick(object sender, MouseButtonEventArgs e) {
            if (tagsList.SelectedItem != null) {
                Tag selectedTag = (Tag)tagsList.SelectedItem;
                string query = "select TOP 100 questions.*, users.display_name AS u_name FROM q_tags JOIN questions ON q_tags.question_id = questions.id JOIN users ON questions.user_id = users.id WHERE q_tags.tag_id = " + selectedTag.Id + " ORDER BY questions.score DESC";
                QuestionsViewModel questionVM = new QuestionsViewModel(query);
                this.mainWindow.MainFrame.NavigationUIVisibility = NavigationUIVisibility.Hidden;
                this.mainWindow.MainFrame.Navigate(new QuestionsListPage(questionVM));
            }
        }
        
    }
}
