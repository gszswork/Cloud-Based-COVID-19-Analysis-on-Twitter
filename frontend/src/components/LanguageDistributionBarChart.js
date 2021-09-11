/**
 * The bar chart of language distribution info on AURIN.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import React from 'react'
import Chart from 'react-apexcharts'

class LanguageDistributionBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [],
        options: {
          chart: {
            type: 'bar',
            height: 500,
          },
          plotOptions: {
            bar: {
              horizontal: true,
            },
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          title: {
            text: ''
          },
          noData: {
            text: 'Loading...'
          },
          xaxis: {
            categories: [],
          },
          yaxis: {
            title: {
              text: undefined
            },
          },
          fill: {
            opacity: 1
          },
          legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetX: 40
          }
        },
      
      
      };
    }

    componentDidMount(){
        this.data = this.props.data.seires[0].data.slice(0, -2)
        this.series = [{data: this.data}]
        this.categories = this.props.data.categories.slice(0, -2)
        this.setState({
            series: this.series,
            options: {
                ...this.state.options,
                xaxis: {
                  ...this.state.options.xaxis, 
                    categories: this.categories,
                },
                title: {
                    ...this.state.options.xais,
                    text: this.props.name
                }
                }
        })
    }

    render() {
      return (
        <div className="app">
        <div className="row">
          <div className="mixed-chart">
            <Chart
              options={this.state.options}
              series={this.state.series}
              type="bar"
              width="800"
            />
          </div>
        </div>
      </div>
      );
    }
  }
export default LanguageDistributionBarChart;