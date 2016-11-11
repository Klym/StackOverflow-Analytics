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
using StackOverflow_Analytics.View;

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for QuestionsListPage.xaml
    /// </summary>
    public partial class QuestionsListPage : Page {

        private MainWindow mainWindow;

        public QuestionsListPage() {
            InitializeComponent();
        }

        private void Page_Loaded(object sender, RoutedEventArgs e) {
            this.mainWindow = (MainWindow)Window.GetWindow(this);
        }

        private void questionsList_MouseDoubleClick(object sender, MouseButtonEventArgs e) {
            Question selectedQuestion = (Question)questionsList.SelectedItem;
            this.mainWindow.MainFrame.NavigationUIVisibility = NavigationUIVisibility.Hidden;
            if (selectedQuestion != null) {
                this.mainWindow.MainFrame.Navigate(new QuestionViewPage(selectedQuestion));
            }
        }
        
    }
}
