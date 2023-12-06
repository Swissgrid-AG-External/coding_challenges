Hi X!

Our intern wrote an API app for a db (I bet he just copied it from the internet). It is so greate that now we would like to host it in the azure. Your tasks as platform engineer are:

1. Design architector of such a solution in azure
    - you are free to choose any azure services you want
    - what matters is: security, scalability, resilience, automation, low maintenance
2. Implement it in terraform or other IaC tool
3. Create a CI/CD pipeline for it (github actions preferred)
4. Review code and correct (or just point out) bad practices
5. Present you decisions, development environment 

To your disposal you have :
- Azure resource group - [swg-poc-01-coding-challenge-XX-rg](https://portal.azure.com/) (you have contributor permissions, let us know if you hit any limits - e.g quota or you need register a provider) 
- github repo - you can commit your code here
- service principal (swg-poc-01-coding-challenge-XX-spi) with owner permissions to the resource group (all necessary credentials are in the github secrets / variables)

Do not spend more than 8 hours on this - if you run out of time (it is totaly fine - the task is big so you need to als make decission what is more important), just describe what you would do next.

Good luck!