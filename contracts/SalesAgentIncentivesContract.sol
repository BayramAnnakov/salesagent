// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SalesAgentIncentives {

    struct Job {
        address payable salesAgent;
        uint paymentAmount;
        uint bonusAmount;
        uint bonusThreshold;
        uint performanceScore;
        bool jobCompleted;
        bool paymentReleased;
    }

    address public owner;
    mapping(uint => Job) public jobs; // Mapping from job ID to Job struct
    uint public jobCount = 0;

    event JobCreated(uint jobId);
    event JobCompleted(uint jobId, uint score);
    event PaymentReleased(uint jobId, uint amount);
    event BonusReleased(uint jobId, uint bonus);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    // Function to create a new job
    function createJob(address payable _salesAgent, uint _paymentAmount, uint _bonusAmount, uint _bonusThreshold) public onlyOwner {
        jobs[jobCount] = Job({
            salesAgent: _salesAgent,
            paymentAmount: _paymentAmount,
            bonusAmount: _bonusAmount,
            bonusThreshold: _bonusThreshold,
            performanceScore: 0,
            jobCompleted: false,
            paymentReleased: false
        });
        emit JobCreated(jobCount);
        jobCount++;
    }

    // To fund a specific job
    function fundJob(uint _jobId) public payable onlyOwner {
        require(msg.value == jobs[_jobId].paymentAmount + jobs[_jobId].bonusAmount, "Incorrect funding amount");
    }

    // Function to mark a job as completed and set the performance score
    function completeJob(uint _jobId, uint _performanceScore) public onlyOwner {
        Job storage job = jobs[_jobId];
        require(!job.jobCompleted, "Job is already marked as completed.");
        job.jobCompleted = true;
        job.performanceScore = _performanceScore;
        emit JobCompleted(_jobId, _performanceScore);
    }

    // Function to release payment for a job based on performance
    function releasePayment(uint _jobId) public onlyOwner {
        Job storage job = jobs[_jobId];
        require(job.jobCompleted, "Job is not yet completed.");
        require(!job.paymentReleased, "Payment is already released.");
        require(address(this).balance >= job.paymentAmount, "Insufficient contract balance.");

        job.paymentReleased = true;
        job.salesAgent.transfer(job.paymentAmount);
        emit PaymentReleased(_jobId, job.paymentAmount);

        // Check if performance score exceeds the threshold for bonus
        if(job.performanceScore >= job.bonusThreshold && address(this).balance >= job.bonusAmount) {
            job.salesAgent.transfer(job.bonusAmount);
            emit BonusReleased(_jobId, job.bonusAmount);
        }
    }

    // Function to retrieve contract balance (for testing and verification)
    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }
}
