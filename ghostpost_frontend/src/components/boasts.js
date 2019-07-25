import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';


class BoastFilter extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            boasts: [],
        };
        this.loadBoasts = this.loadBoasts.bind(this)
    }

    componentWillMount() {
        this.loadBoasts();
    }

    async loadBoasts() {
        const promise = await axios.get("http://localhost:8000/apiBaRs/")
        const status = promise.status;
        if(status === 200) {
            const data = promise.data;
            this.setState({boasts:data});
        }
    }
    render () {
        return (
            <React.Fragment>
                <h1>Boasts</h1>
                <div className="boast">
                    {this.state.boasts.map((message)=>{return <p>{message.boasts}</p>})}
                </div>
                <p><Link to="/">Home</Link></p>

            </React.Fragment>
        )
    }
}

export default BoastFilter;