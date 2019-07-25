import React from "react";
import axios from "axios";
import { Link } from 'react-router-dom';

class RoastFilter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
        roasts:[],
        };
        this.loadRoasts = this.loadRoasts.bind(this);
      }
    
      componentWillMount() {
        this.loadRoasts();
      }

      async loadRoasts()
  {
    const promise = await axios.get("http://localhost:8000/apiBaRs/");
    const status = promise.status;
    if(status===200)
    {
      const data = promise.data;
      this.setState({roasts:data});
    }
  }
    render() {
    return (
        <React.Fragment>
            <h1>Roasts</h1>
            <div className="roast">
                {this.state.roasts.map((message)=>{return <p>{message.roasts}</p>})}
            </div>
            <p><Link to="/">Home</Link></p>
        </React.Fragment>
    )
    }
}

export default RoastFilter;