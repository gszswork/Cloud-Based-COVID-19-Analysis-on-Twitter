/**
 * The donut chart of population distribution info on AURIN.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import React from 'react'
import ReactApexChart from 'react-apexcharts';
import './PopulationDistributionDonutChart.css'

class PopulationDistributionDonutChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [],
        options: {
          chart: {
            type: 'donut',
          },
          labels: [],
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: 200
              },
              legend: {
                position: 'bottom'
              }
            }
          }],
          plotOptions: {
            pie: {
              donut: {
                labels: {
                  show: true,
                  total: {
                    showAlways: true,
                    show: true
                  }
                }
              }
            }
          },
      }
    }
    }

    componentDidMount(){
        this.setState({
            series: this.props.data.data.count,
            options: {
            ...this.state.options,
            labels: this.props.data.data.labels
            }
        })
    }

    render() {
      return (
        <div className="donut">
            <div className="title">{this.props.name}</div>
            <ReactApexChart options={this.state.options} series={this.state.series} type="donut" />
        </div>
      );
    }
  }
export default PopulationDistributionDonutChart;