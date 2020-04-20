import React, { Component } from 'react';
import UrlsService from './urlServices';

const urlService = new UrlsService();

class CreateUrl extends Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
      }

      handleCreate(){
        urlService.createUrl(
          {
            "name": this.refs.link.value,
        }).then((result)=>{
          alert("Customer created!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }

      handleSubmit(event) {
        const { match: { params } } = this.props;
        this.handleCreate();
        event.preventDefault();
      }

      render() {
        return (
          <form onSubmit={this.handleSubmit}>
              <div className="form-group">
                    <label>First Name:</label>
                    <input className="form-control" type="text" ref='link' />
                    <input className="btn btn-primary" type="submit" value="Submit" />
              </div>
          </form>
        );
      }
}

export default CreateUrl;