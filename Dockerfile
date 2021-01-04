FROM alpine

RUN apk update && apk upgrade && apk add vsftpd && apk add openrc --no-cache

CMD ["tail", "-f", "/dev/null"]