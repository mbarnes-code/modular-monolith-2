# Software Forensic Kit Docker Image
FROM openjdk:8-jre-alpine

# Metadata
LABEL maintainer="Software Forensic Kit Team"
LABEL description="Binary analysis toolkit for Java applications"
LABEL version="1.0.0"

# Install required packages
RUN apk add --no-cache \
    bash \
    openssh-client \
    ca-certificates \
    && rm -rf /var/cache/apk/*

# Create application directory
WORKDIR /app

# Create data directory for analysis input/output
RUN mkdir -p /data

# Copy the built JAR file
COPY apps/software-forensic-kit-service/target/software-forensic-kit-*-jar-with-dependencies.jar /app/software-forensic-kit.jar

# Create non-root user for security
RUN addgroup -g 1001 forensics && \
    adduser -D -u 1001 -G forensics forensics

# Change ownership of application files
RUN chown -R forensics:forensics /app /data

# Switch to non-root user
USER forensics

# Set default Java options for container environment
ENV JAVA_OPTS="-Xmx2g -XX:+UseG1GC -Djava.io.tmpdir=/tmp"

# Default command shows help
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/software-forensic-kit.jar \"$@\"", "--"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD java $JAVA_OPTS -jar /app/software-forensic-kit.jar --version || exit 1

# Expose no ports (command line tool)
# EXPOSE

# Volume for data input/output
VOLUME ["/data"]