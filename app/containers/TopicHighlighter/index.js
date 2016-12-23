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

import { colors } from 'utils/colors';
import HighlightTool from 'components/HighlightTool';
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

  // Babel plugin transform-class-properties allows us to use
  // ES2016 property initializer syntax. So the arrow function
  // will bind 'this' of the class. (React.createClass does automatically.)
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
              <div className="article" key={this.props.article.articleId}>
                <div className='article__header-text'>
                </div>
                <div id='article-container'>
                  <HighlightTool
                    text={this.props.article.text}
                    topics={this.props.topics.results}
                    colors={colors}
                    currentTopicId={this.props.currentTopicId}
                  />
                </div>
              </div>
            </ReactCSSTransitionsGroup>
            <br/>
            <button onClick={this.onSaveAndNext}>Save and Next</button>
            <div className="space"></div>
        </div>
      </ReactCSSTransitionsGroup>
    );
  }
};
