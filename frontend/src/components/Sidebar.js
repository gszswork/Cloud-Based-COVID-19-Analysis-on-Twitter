import React from 'react';
import { bubble as Menu } from 'react-burger-menu';
import './Sidebar.css'
import 'react-calendar/dist/Calendar.css';
import Grid from '@material-ui/core/Grid';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardDatePicker,
  KeyboardTimePicker,
} from '@material-ui/pickers';

import { Button, ButtonGroup, Box, Switch, FormControl, FormLabel, FormControlLabel, Radio, RadioGroup, Select, MenuItem} from '@material-ui/core'
import 'date-fns';
import Popup from 'reactjs-popup';

import history from '../history'
import TopWordBarChart from './TopWordBarChart';
import { withStyles } from '@material-ui/core/styles';

// const language_dictionary = {
//   "Arabic": "ar",
//   "Danish": "da",
//   "German": "de",
//   "English": "en",
//   "Spanish": "es",
//   "Estonian": "et",
//   "Finnish": "fi",
//   "French": "fr",
//   "Hindi": "hi",
// "Hungarian": "hu",
// "Indonesian": "in",
// "Icelandic": "is",
// "Italian": "it",
// "Japanese": "ja",
// "Korean": "ko",
// "Lithuanian": "lt",
// "Latvian": "lv",
// "Dutch": "nl",
// "Norwegian": "no",
// "Polish": "pl",
// "Portuguese": "pt",
// "Russian": "ru",
// "Slovenian": "sl",
// "Swedish": "sv",
// "Thai": "th",
// "Tagalog": "tl",
// "Turkish": "tr",
// "Vietnamese": "vi",
// "Chinese": "zh",
// }

const AntSwitch = withStyles((theme) => ({
  root: {
    width: 28,
    height: 16,
    padding: 0,
    display: 'flex',
  },
  switchBase: {
    padding: 2,
    color: theme.palette.grey[500],
    '&$checked': {
      transform: 'translateX(12px)',
      color: theme.palette.common.white,
      '& + $track': {
        opacity: 1,
        backgroundColor: theme.palette.primary.main,
        borderColor: theme.palette.primary.main,
      },
    },
  },
  thumb: {
    width: 12,
    height: 12,
    boxShadow: 'none',
  },
  track: {
    border: `1px solid ${theme.palette.grey[500]}`,
    borderRadius: 16 / 2,
    opacity: 1,
    backgroundColor: theme.palette.common.white,
  },
  checked: {},
}))(Switch);

class Sidebar extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      scenario: null,
      selectedStartDate: new Date('2020-10-02T00:00:00'),
      startDate: new Date('2020-10-01T00:00:00'),
      endDate: new Date('2021-01-13T00:00:00'),
      isWordOrTag: false,
      language: "ar",
    };
  }

  sendData = (value) => {
    this.props.parentCallback(value);
  };

  handleStartDateChange = (date) => {
    this.setState({
      selectedStartDate: date,
    });
  };

  handleScenarioChange = (event) => {
    this.setState({
      scenario: event.target.value,
    });
    this.sendData({
      scenario: event.target.value,
      language: this.state.language})
  };

  handleSwitchChange = (event) => {
    this.setState({
      isWordOrTag: event.target.checked
    })
  }

  handleLanguageChange =( event) => {
    this.setState({
      language: event.target.value,
    });
    this.sendData({
      scenario: this.state.scenario,
      language:event.target.value
    })
  }

  render() {
  return (
    <Menu>
      <ButtonGroup fullWidth variant="text" color="primary" aria-label="text primary button group">
      <Button variant="outlined" color="primary"
        onClick={() => history.push('/')}>
        Map
      </Button>
      <Button variant="outlined" color="primary"
        onClick={() => history.push('/Analysis')}>
        Analysis
      </Button>
      </ButtonGroup>

      <MuiPickersUtilsProvider utils={DateFnsUtils}>

      <Grid>
        {/* scenario selection */}
        <FormControl component="fieldset">
          <FormLabel component="legend">Scenario</FormLabel>
          <RadioGroup aria-label="scenario" name="scenario" value={this.state.scenario} onChange={this.handleScenarioChange}>
            <FormControlLabel value="Victoria Covid" control={<Radio />} label="Victoria Covid" />
            <FormControlLabel value="Tweet Heatmap" control={<Radio />} label="Tweet Heatmap" />
            <FormControlLabel value="Tweet Top words" control={<Radio />} label="Tweet Top Words/Tags" />
            <FormControlLabel value="Languages" control={<Radio />} label="Languages" />
          </RadioGroup>
        </FormControl>
      </Grid>


      <Box visibility={this.state.scenario === "Languages" ? "visible": "hidden"}>
      <Grid>
      <FormControl>
        <Select
          labelId="language-native-simple"
          id="language-simple-select"
          value={this.state.language}
          onChange={this.handleLanguageChange}
        >
          {/* this is not working...
          {language_dictionary.map(((item) => (
            <MenuItem value={item.value}>{item.key}</MenuItem>
          )))} */}
          <MenuItem value={"ar"}>Arabic</MenuItem>
          <MenuItem value={"da"}>Danish</MenuItem>
          <MenuItem value={"de"}>German</MenuItem>
          <MenuItem value={"en"}>English</MenuItem>
          <MenuItem value={"es"}>Spanish</MenuItem>
          <MenuItem value={"et"}>Estonian</MenuItem>
          <MenuItem value={"fi"}>Finnish</MenuItem>
          <MenuItem value={"fr"}>French</MenuItem>
          <MenuItem value={"hi"}>Hindi</MenuItem>
          <MenuItem value={"hu"}>Hungarian</MenuItem>
          <MenuItem value={"in"}>Indonesian</MenuItem>
          <MenuItem value={"is"}>Icelandic</MenuItem>
          <MenuItem value={"it"}>Italian</MenuItem>
          <MenuItem value={"ja"}>Japanese</MenuItem>
          <MenuItem value={"ko"}>Korean</MenuItem>
          <MenuItem value={"lt"}>Lithuanian</MenuItem>
          <MenuItem value={"lv"}>Latvian</MenuItem>
          <MenuItem value={"nl"}>Dutch</MenuItem>
          <MenuItem value={"no"}>Norwegian</MenuItem>
          <MenuItem value={"pl"}>Polish</MenuItem>
          <MenuItem value={"pt"}>Portuguese</MenuItem>
          <MenuItem value={"ru"}>Russian</MenuItem>
          <MenuItem value={"sl"}>Slovenian</MenuItem>
          <MenuItem value={"sv"}>Swedish</MenuItem>
          <MenuItem value={"th"}>Thai</MenuItem>
          <MenuItem value={"tl"}>Tagalog</MenuItem>
          <MenuItem value={"tr"}>Turkish</MenuItem>
          <MenuItem value={"vi"}>Vietnamese</MenuItem>
          <MenuItem value={"zh"}>Chinese</MenuItem>
        </Select>
      </FormControl>
      </Grid>
      </Box>

  <Box visibility={this.state.scenario === "Tweet Top words" ? "visible": "hidden"}>

  <Grid component="label" container alignItems="center" spacing={2}>
          <Grid item >word</Grid>
          <Grid item>
            <AntSwitch checked={this.state.isWordOrTag} onChange={this.handleSwitchChange} name="isWordOrTag" />
          </Grid>
          <Grid item>tag</Grid>
        </Grid>

      <Grid container justify="space-around" >
      <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="start-date-picker-inline"
          label="Start date"
          maxDate={this.state.endDate}
          minDate={this.state.startDate}
          value={this.state.selectedStartDate}
          onChange={this.handleStartDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        />
        <KeyboardTimePicker
          margin="normal"
          id="start-time-picker"
          label="Start time"
          value={this.state.selectedStartDate}
          onChange={this.handleStartDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        />
        {/* <KeyboardDatePicker
          disableToolbar
          variant="inline"
          format="MM/dd/yyyy"
          margin="normal"
          id="end-date-picker-inline"
          label="End date"
          minDate={this.state.selectedStartDate}
          maxDate={this.state.endDate}
          value={this.state.selectedEndDate}
          onChange={this.handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change date',
          }}
        /> */}
        {/* <KeyboardTimePicker
          margin="normal"
          id="end-time-picker"
          label="End time"
          value={this.state.selectedEndDate}
          onChange={this.handleEndDateChange}
          KeyboardButtonProps={{
            'aria-label': 'change time',
          }}
        /> */}
        </Grid>

    <Grid>
      <Popup trigger={<Button variant="outlined" color="primary">
        Apply
      </Button>} modal>
      <TopWordBarChart 
        startDate={this.state.selectedStartDate} 
        isWordOrTag={this.state.isWordOrTag}/>
      </Popup>
    </Grid>

    </Box>
    </MuiPickersUtilsProvider>
    </Menu>

  );
};
}

export default Sidebar;