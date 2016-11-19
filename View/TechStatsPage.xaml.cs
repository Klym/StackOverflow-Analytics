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
    /// Interaction logic for TechStats.xaml
    /// </summary>
    public partial class TechStatsPage : Page {

        public SeriesCollection SeriesCollection { get; set; }
        public string[] Labels { get; set; }
        //public Func<double, string> YFormatter { get; set; }

        public TechStatsPage() {
            InitializeComponent();

            SeriesCollection = new SeriesCollection();

            Labels = new[] { "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015" };

            string[] technologies = new string[] { "C#", "C++", "Java", "Python", "PHP", "JavaScript" };
            for (int i = 0; i < technologies.Length; i++) {
                TechStats stat = new TechStats(technologies[i]);
                SeriesCollection.Add(new LineSeries {
                    Title = technologies[i],
                    Values = stat.Values,
                });
            }

            DataContext = this;
        }
    }
}
