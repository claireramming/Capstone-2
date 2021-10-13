import './App.css'
import React, {useState} from 'react'
import Form from './Form'

function App() {
  const [prediction, setPrediction] = useState()

  return (
    <>
      <Form setPred={setPrediction}/>
      {prediction ? <h2>${prediction}</h2> : ''}
    </>
  )
}

export default App;
