import React, { Component } from 'react';
import './App.css';
import './style.css'

//General class design for individual components 
class APIComponent extends Component{
    constructor(props){
        super(props);
        this.state = {
          error: null,
          Data: [],       
        }
}

//Used to render every second of data
componentDidMount() {
  
    setInterval(() => {
     this.loadData()
    }, 1000);
   }


//Fetches the data from an API route
async loadData(){
    try{
        fetch('http://IP/API_ROUTE/.../')
        .then(res => res.json())
        .then(
          (res) => {
            this.setState({
              Data: res
            });
          },
          (error) => {
            this.setState({
              error: true
            });
          }
        )
      }
      catch(e){
        console.log(e)
      }
}



render() {
    return(

<div class="container-fluid ScrollContainer">
  <row>
    <div class="card-group">

      <div class="col-sm-4 card text-center">
        <div class="card-header bg-info" >Average Data of last 24 hours</div>
        <div class="card-body bg-success">{this.state.Data[0]}</div> 
      </div>
    </div>
  </row>
</div>
      );
}

}
export default APIComponent;