import React, {useState} from 'react';
import logo from './logo.svg';
import './App.css';



const getCookie = (name) => {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
    else return null;
}

let params = {credentials: 'same-origin', method: 'POST', headers : {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                "Content-Type": "application/json"
                },
//                body: JSON.stringify(data)
            }


function post_request(url, data){
    let p_data = params;
    p_data['body'] = JSON.stringify(data);
    fetch(url, params).then(function(response){
        if (!response.ok){
            return response.json().then(json => {throw json});
        }
        return response.json()
    }).then((json) => {
        console.log(json);
//        that.props.onHide();
//        that.props.add_attachment(json);
    }).catch(function(err){
//        that.props.update_errors(err);
        console.log(err);
    });

}



function App() {
    let margin_style = {margin: '20px'}
    let display_style = {display: 'block'};

    const [login_name, set_login_name] = useState('');
    const [login_password, set_login_password] = useState('');

    const handleChange = event => set_login_name(event.target.value);



    let url = '/user';
    let data = {};

  return (
    <div className="App">
      <div> Welcome to Tekkon App </div>

      <div style={margin_style}>
          <form id="login-form">
              <input type="text" placeholder="Username" style={display_style}/>
              <input type="password" placeholder="Password" style={display_style}/>

              <input type="submit" value="Login" style={display_style}/>
          </form>
      </div>

      <div style={margin_style}>
          <form id="registration-form">
              <input type="text" placeholder="First Name" style={display_style}/>
              <input type="text" placeholder="Last Name" style={display_style}/>
              <input type="text" placeholder="Email" style={display_style}/>

              <input type="submit" value="Register" style={display_style}/>
          </form>
          </div>
      </div>
  );
}

export default App;
