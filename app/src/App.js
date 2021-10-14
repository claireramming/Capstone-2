import './App.css'
import React, {useState} from 'react'
import Header from './Header'
import Form from './Form'
import Logo from './Logo'

function App() {
  const [prediction, setPrediction] = useState()

  return (
    <div className='main-container'>
      <Header />
      <p className='instructions'>
        Please select your rental criteria below:
      </p>
      <Form setPred={setPrediction}/>
      {prediction ? <h2 className='result'>Fair fare found: ${prediction}/night</h2> : ''}
      <footer><Logo/></footer>
    </div>
  )
}

export default App;
