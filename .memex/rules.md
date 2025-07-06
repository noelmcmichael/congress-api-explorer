# Development Rules and Guidelines

## Project Standards

### Code Organization
- Follow the established directory structure
- Keep related functionality together
- Use descriptive module and function names
- Maintain clear separation of concerns

### API Design Principles
- **Rate Limit Respect**: Always consider the 5000/day Congress API limit
- **Caching First**: Implement caching for all API responses
- **Error Handling**: Graceful degradation with informative error messages
- **Type Safety**: Use Pydantic models for all data structures

### MCP Integration Standards
- Follow official MCP protocol specifications
- Implement proper error handling for MCP operations
- Provide clear tool descriptions and parameter documentation
- Use structured responses with appropriate metadata

### Development Practices
- **Incremental Development**: Build and test components separately
- **Commit Early**: Commit after each successful step
- **Document Progress**: Update README.md with each milestone
- **Test Coverage**: Write tests for all critical functionality

### Code Quality
- Use type hints throughout
- Follow PEP 8 style guidelines
- Write docstrings for all public functions
- Keep functions focused and single-purpose

### Git Workflow
- Use descriptive commit messages
- Include Memex attribution in commits
- Create feature branches for major changes
- Tag releases with semantic versioning

### Security
- Never commit API keys or sensitive data
- Use environment variables for configuration
- Implement proper authentication patterns
- Validate all external inputs

### Performance
- Implement request batching where possible
- Use async/await for I/O operations
- Monitor and log API usage
- Optimize for common use cases

## Congress API Specific Guidelines

### Request Strategy
- Prioritize current hearings over historical data
- Batch related requests to minimize API calls
- Use appropriate date ranges to limit results
- Cache aggressively with smart TTL policies

### Data Handling
- Validate all API responses
- Handle incomplete or missing data gracefully
- Normalize data structures for consistency
- Log data quality issues for investigation

### Rate Limiting
- Track request counts and timing
- Implement backoff strategies for rate limits
- Queue requests during peak usage
- Monitor daily/hourly usage patterns

## MCP Server Guidelines

### Tool Design
- Create focused, single-purpose tools
- Provide clear parameter descriptions
- Return structured, consistent responses
- Include helpful error messages

### Resource Management
- Implement proper resource cleanup
- Handle connection failures gracefully
- Use appropriate timeout values
- Log resource usage for monitoring

### Client Integration
- Follow MCP protocol specifications exactly
- Provide clear tool documentation
- Handle client disconnections properly
- Support concurrent client connections

## Testing Strategy

### Unit Tests
- Test all API client functions
- Validate data model serialization
- Test error handling scenarios
- Mock external dependencies

### Integration Tests
- Test full MCP server workflows
- Validate API rate limiting
- Test caching behavior
- Verify error propagation

### Performance Tests
- Measure response times
- Test under rate limit conditions
- Validate memory usage
- Test concurrent request handling

## Documentation Requirements

### Code Documentation
- Docstrings for all public functions
- Type hints for all parameters
- Usage examples in docstrings
- Clear parameter descriptions

### API Documentation
- Document all MCP tools and resources
- Include usage examples
- Explain rate limiting behavior
- Document configuration options

### User Documentation
- Clear setup instructions
- Configuration examples
- Usage tutorials
- Troubleshooting guides

## Deployment Considerations

### Configuration Management
- Use environment variables for settings
- Provide sensible defaults
- Document all configuration options
- Implement configuration validation

### Monitoring and Logging
- Log all API requests and responses
- Monitor rate limit usage
- Track error rates and types
- Implement health checks

### Error Handling
- Provide clear error messages
- Log errors with sufficient context
- Implement retry logic where appropriate
- Handle network failures gracefully

## Quality Assurance

### Code Review Checklist
- [ ] Follows established patterns
- [ ] Includes appropriate tests
- [ ] Updates documentation
- [ ] Handles errors gracefully
- [ ] Respects rate limits
- [ ] Uses proper typing
- [ ] Includes logging
- [ ] Follows security guidelines

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Configuration validated
- [ ] Performance tested
- [ ] Security reviewed
- [ ] Deployment tested
- [ ] Monitoring configured
- [ ] Rollback plan prepared