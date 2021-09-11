/**
 * The heat words/tags as well as sentiment score info calculated by backend, during a certain timeframe.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import React from 'react'
import Chart from 'react-apexcharts'
import './TopWordBarChart.css'
import { Emoji } from 'emoji-mart'

class TopWordBarChart extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        sentiment: ':question:',
        series:  [],
        options: {
          chart: {
            type: 'bar',
            height: 500,
          },
          plotOptions: {
            bar: {
              horizontal: false,
            },
          },
          stroke: {
            width: 1,
            colors: ['#fff']
          },
          title: {
            text: 'Tweet Top Words/Tags'
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

    getSentimentLevel = (score) => {
      if(score < -0.2){
        return ":rage:"
      } else if (score >= -0.2 && score < -0.1){
        return ":worried:"
      } else if (score >= -0.1 && score < 0){
        return ":pensive:"
      } else if (score >= 0 && score < 0.1){
        return ":neutral_face:"
      } else if (score >= 0.1 && score < 0.2){
        return ":slightly_smiling_face:"
      } else if (score >= 0.2 && score < 0.3){
        return ":grin:"
      } else if (score >= 0.3){
        return ":smiling_face_with_3_hearts:"
      } 
    }

    componentDidMount(){
        const year = this.props.startDate.getFullYear()
        const month = this.props.startDate.getMonth()
        const day = this.props.startDate.getDate()
        const hours = this.props.startDate.getHours()
        const startDate = String(this.props.startDate).slice(4, 24).replaceAll(' ', '-')
        var date = new Date(year, month, day, hours);
        date.setDate(this.props.startDate.getDate() + 1)
        const endDate = String(date).slice(4, 24).replaceAll(' ', '-')
        const isWordOrTag = this.props.isWordOrTag ? 'tag' : 'word'
        fetch(`http://172.26.133.226:8000/api/tweet/top/${isWordOrTag}/10/${startDate}/${endDate}`)
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          sentiment: this.getSentimentLevel(result.sentiment_score),
          sentiment_score: result.sentiment_score.toFixed(5),
          series: result.series,
          options: {
            ...this.state.options,
            xaxis: {
              ...this.state.options.xaxis, 
                categories: result.name
              }
            }
        })
      },
      (error) => {
        this.setState({
            isLoaded: true,
            error
          });
      })
    }

    render() {
      return (
        <div className="app">
        <div className="row">
          <div className="sentiment">
            Sentiment level:
            <Emoji emoji={this.state.sentiment} size={50} />
            ({this.state.sentiment_score})
          </div>
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
export default TopWordBarChart;