import React from 'react';
import '../styles/ResultCard.css';

/**
 * Card component for displaying research results
 * @param {Object} props
 * @param {string} props.title - Card title
 * @param {string|Array} props.content - Card content
 * @param {boolean} props.highlight - Whether to highlight this card
 */
function ResultCard({ title, content, highlight = false }) {
    const cardClass = highlight ? 'result-card highlight' : 'result-card';

    // Handle array content (for sources)
    const renderContent = () => {
        if (Array.isArray(content)) {
            if (content.length === 0) {
                return <p className="no-content">No sources available</p>;
            }
            return (
                <ul className="sources-list">
                    {content.map((item, index) => (
                        <li key={index}>
                            <a href={item} target="_blank" rel="noopener noreferrer">
                                {item}
                            </a>
                        </li>
                    ))}
                </ul>
            );
        }

        // Handle object content (for integration status)
        if (typeof content === 'object' && content !== null) {
            return (
                <div className="status-grid">
                    {Object.entries(content).map(([key, value]) => (
                        <div key={key} className="status-item">
                            <span className="status-key">{key}:</span>
                            <span className={`status-value ${value === true ? 'enabled' : ''}`}>
                                {String(value)}
                            </span>
                        </div>
                    ))}
                </div>
            );
        }

        // Handle string content
        return <p className="content-text">{content || 'No content available'}</p>;
    };

    return (
        <div className={cardClass}>
            <h3 className="card-title">{title}</h3>
            <div className="card-content">
                {renderContent()}
            </div>
        </div>
    );
}

export default ResultCard;
