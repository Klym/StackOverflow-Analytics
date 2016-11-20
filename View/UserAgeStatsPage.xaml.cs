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
using LiveCharts;
using LiveCharts.Wpf;

namespace StackOverflow_Analytics {
    /// <summary>
    /// Interaction logic for UserAgeStatsPage.xaml
    /// </summary>
    public partial class UserAgeStatsPage : Page {

        public SeriesCollection SeriesCollection { get; set; }
        public Func<ChartPoint, string> PointLabel { get; set; }

        public UserAgeStatsPage() {
            InitializeComponent();

            PointLabel = chartPoint =>
                string.Format("{0} ({1:P})", chartPoint.Y, chartPoint.Participation);

            SeriesCollection = new SeriesCollection();
            string[] labels = new[] { "18-25", "26-35", "36-45", "46-60", "60-100"};

            for (int i = 0; i < labels.Length; i++) {
                string[] ages = labels[i].Split('-');
                UserAgeStats stats = new UserAgeStats(int.Parse(ages[0]), int.Parse(ages[1]));
                if (i + 1 == labels.Length) {
                    labels[i] = "60+";
                }
                SeriesCollection.Add(new PieSeries {
                    Title = labels[i],
                    Values = stats.Values,
                    DataLabels = true,
                    LabelPoint = PointLabel
                });
            }

            DataContext = this;
        }
    }
}
