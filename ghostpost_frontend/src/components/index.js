import React, { Component } from 'react';
import {Form, TextArea, Button} from 'semantic-ui-react';
import axios from 'axios';
import { Link } from 'react-router-dom';
// import List from './list.js'


export default class Boast extends Component {
    constructor(props) {
        super(props);
        this.state = {
            boasts: [],
        };
        this.loadboasts = this.loadboasts.bind(this)
    }
    componentWillMount() {
        this.loadboasts();
    }
    handleSubmitBoast = event => {
        fetch('http://localhost:8000/apiBaRs/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({boasts: this.state.boast,
                                roasts: 'no roasts'})

        });
    window.location.reload()};

    handleSubmitRoast = event => {
        fetch('http://localhost:8000/apiBaRs', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({roasts: this.state.roast,
                                boasts: 'no boasts'})
    })
    window.location.reload()};

    handleOnChangeRoast = event => {
        this.setState({
            roast: event.target.value
        });
    };

    handleOnChangeBoast = event => {
        this.setState({
            boast: event.target.value
        });
    };

    // messagesSortedByDate = (messages) => {
    //     return messages.sort((a, b) => b.dateCreated - a.dateCreated).reverse()
    // }

    async loadboasts() {
        const promise = await axios.get("http://localhost:8000/apiBaRs/");
        const status = promise.status;
        if(status === 200) {
            const data = promise.data;
            this.setState({boasts:data});
        }
    }

    render() {
        return (
            <React.Fragment>
                <div className="main">
                    <h1>Boasts and Roasts</h1>
                    <h2>Submit a Boast or Roast</h2>
                    <div className="filters"><Link to="/boasts">BoastList</Link></div>
                    <div className="filters"><Link to="/roasts">RoastList</Link></div>
                    <div className="boastform">
                        <Form>
                            <TextArea
                            placeholder="Create a Boast"
                            onChange={this.handleOnChangeBoast} />
                        </Form>
                    <Button className="submit-button" onClick={this.handleSubmitBoast} type="Submit">
                        Submit
                    </Button>
                    </div>
                    <div className="roastform">
                        <Form>
                            <TextArea
                            placeholder="Create a Roast"
                            onChange={this.handleOnChangeRoast} />
                        </Form>
                    <Button className="submit-button" onClick={this.handleSubmitRoast} type="Submit">
                        Submit
                    </Button>
                    </div>
        {/* {this.messagesSortedByDate(this.boasts.map((message)=>{return <List boasts={message.boasts} roasts={message.roasts} />}))} */}
                </div>
            </React.Fragment>
        )
    }

}
