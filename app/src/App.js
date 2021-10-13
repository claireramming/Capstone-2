import './App.css'
import React, {useState} from 'react'
import Header from './Header'
import Form from './Form'

function App() {
  const [prediction, setPrediction] = useState()

  return (
    <>
      <Header />
      <p className='instructions'>
        Please select your rental criteria below:
      </p>
      <Form setPred={setPrediction}/>
      {prediction ? <h2>${prediction}</h2> : ''}
    </>
  )
}

export default App;
