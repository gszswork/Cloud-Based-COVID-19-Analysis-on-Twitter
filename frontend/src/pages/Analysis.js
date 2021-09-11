/**
 * The analysis page displaying two bar charts.
 * Author: yueying chang
 * Student id: 1183384
 * Team: COMP90024 - team 24
 */

import React from 'react'
import DeathBarChart from '../components/DeathBarChart'
import EmploymentBarChart from '../components/EmploymentBarChart'
 
function Analysis() {
 
  return (
    <div>
      <div>
        <DeathBarChart/>
    </div>
    <div>
      <EmploymentBarChart/>
    </div>
</div>
  )
}

export default Analysis;