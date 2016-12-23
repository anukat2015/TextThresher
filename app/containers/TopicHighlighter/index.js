import React, {Component} from 'react';
import { Link } from 'react-router';
import { bindActionCreators } from 'redux';
import ReactDOM from 'react-dom';
import ReactCSSTransitionsGroup from 'react-addons-css-transition-group';
import { connect } from 'react-redux';

import * as articleActionCreators from 'actions/article';
import * as topicsActionCreators from 'actions/topicPicker';
import * as projectActionCreators from 'actions/project';
import * as taskActionCreators from 'actions/highlightTasks';

const assembledActionCreators = Object.assign({}, articleActionCreators, topicsActionCreators, projectActionCreators, taskActionCreators)

import Article from 'components/Article';
import TopicPicker from 'components/TopicPicker';
import Project from 'components/Project';

import { styles } from './styles.scss';

const mapStateToProps = state => {
  return {
    article: state.article.article,
    saveAndNext: state.article.saveAndNext,
    currentTopicId: state.topicPicker.currentTopicId,
    topics: state.topicPicker.topics,
    highlights: state.highlight.highlights
  };
}

@connect (
  mapStateToProps,
  dispatch => bindActionCreators(assembledActionCreators, dispatch)
)

export class TopicHighlighter extends Component {
  constructor(props) {
    super(props);
  }

  onSaveAndNext = () => {
    this.props.saveAndNext(this.props.highlights);
  }

  componentDidMount() {
    this.props.fetchHighlightTasks();
  }

  componentWillReceiveProps(nextProps) {
  }

  render() {
    // TODO: Detect if done
    // return (<div>DONE</div>)

    let loadingClass = this.props.article.isFetching ? 'loading' : '';

    return (
      <ReactCSSTransitionsGroup transitionName='fadein'
                                transitionAppear
                                transitionAppearTimeout={500}
                                transitionEnterTimeout={500}
                                transitionLeaveTimeout={500}>
        <div className={loadingClass}></div>
        <div className='topic-picker-wrapper'>
          <TopicPicker topics={this.props.topics} />
        </div>
        <div className='article-wrapper'>
            <Project />
            <ReactCSSTransitionsGroup transitionName='fade-between'
                                      transitionAppear
                                      transitionAppearTimeout={500}
                                      transitionEnterTimeout={500}
                                      transitionLeaveTimeout={500}>
              {<Article
                article={this.props.article}
                key={this.props.article.articleId}
                topics={this.props.topics}
                currentTopicId={this.props.currentTopicId}
                postArticleHighlights={this.props.postArticleHighlights}
              />}
            </ReactCSSTransitionsGroup>
            <br/>
            <button onClick={this.onSaveAndNext}>Save and Next</button>
            <div className="space"></div>
        </div>
      </ReactCSSTransitionsGroup>
    );
  }
};
