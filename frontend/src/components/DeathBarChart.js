/**
 * The bar chart displaying the death related info on AURIN.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import React from 'react'
import Chart from 'react-apexcharts'

class DeathBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        series: [],
        options: {
          chart: {
            type: 'bar',
            height: 500,
            stacked: true,
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
            text: 'Provisional Mortality Statistics 2020'
          },
          noData: {
            text: 'Loading...'
          },
          xaxis: {
            categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
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

    componentDidMount() {
        fetch("http://172.26.133.226:8000/api/death/all")
          .then(res => res.json())
          .then(
            (result) => {
              this.setState({
                isLoaded: true,
                series: result.series
              });
            },
            (error) => {
              this.setState({
                isLoaded: true,
                error
              });
            } )
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
export default DeathBarChart;