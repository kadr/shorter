import React from 'react';
import './App.css';

const axios = require('axios');
const session = 'sdjfnhkajhdfas7687sdafasd'
const API_URL = 'http://localhost'



const  urlService  =  new  urlService();


function App() {
  return (
    <div className="App">
      <div className="form">
        <form action="">
          <label>
            Введите ссылку: &nbsp;
            <input type="text" name='url' ref='link' />
          </label>

          <button onClick={urlService.createUrl(this.refs.link.value)}>Отправить</button>
        </form>
      </div>
      <div id='short'></div>
    </div>
  );
}

export default App;
