To build a fintech app in Django that ensures data residency for users from different countries, you'll need to implement a data localization strategy. This strategy involves segregating and storing user data in data centers located within each respective country to comply with data sovereignty and privacy regulations. Here are the steps to achieve this:

1. **Select Data Center Locations:**
   Choose data center locations in each of the three countries where you plan to operate. These data centers should comply with local data residency and privacy laws.

2. **Database Replication:**
   Implement database replication to synchronize user data across data centers. Django supports various databases (e.g., PostgreSQL, MySQL) that allow for replication setups. Configure master-slave or multi-master replication based on your requirements and database choice.

3. **Geographical Load Balancing:**
   Use a content delivery network (CDN) or a global load balancer to route user requests to the nearest data center. This ensures that users' requests are directed to the appropriate data center based on their geographical location.

4. **Data Partitioning:**
   Partition the database tables based on country or region. Each partition corresponds to a specific data center. Django's database routing can be used to direct queries to the appropriate database based on the user's country.

   ```python
   class CountryDatabaseRouter:
       def db_for_read(self, model, **hints):
           if model._meta.app_label == 'your_app':
               # Determine the user's country and return the database alias accordingly
               return 'db_country_us'  # for the US, for example
           return 'default'
   ```

5. **Data Encryption:**
   Encrypt sensitive user data at rest and in transit using industry-standard encryption protocols. Django supports various encryption libraries and tools to achieve this.

6. **User Consent and Privacy Settings:**
   Provide users with the option to specify their country of residence and consent to data localization practices. Ensure that your app complies with local privacy regulations and allows users to control their data.

7. **Audit Logs and Compliance Reporting:**
   Implement robust audit logging to track data access and changes. This is crucial for compliance and transparency. Be prepared to generate compliance reports for regulatory authorities as needed.

8. **Compliance with Data Protection Regulations:**
   Familiarize yourself with and adhere to data protection regulations in each country, such as GDPR in Europe or CCPA in California. Implement features like data access requests and data deletion requests to comply with these regulations.

9. **Regular Compliance Audits:**
   Conduct regular compliance audits to ensure that your data residency and privacy practices align with local laws and regulations. Be prepared to make adjustments as regulations change.

10. **Data Backup and Disaster Recovery:**
    Implement robust data backup and disaster recovery plans for each data center. Ensure that data can be restored in case of hardware failures or other unforeseen incidents.

11. **Secure Authentication and Authorization:**
    Implement strong authentication and authorization mechanisms to ensure that only authorized personnel can access user data.

12. **Regular Security Testing:**
    Perform regular security assessments, including penetration testing and code reviews, to identify and mitigate potential vulnerabilities.

13. **Legal Counsel:**
    Consult with legal experts to ensure that your data residency and privacy practices comply with local laws and regulations.

Building a fintech app with data residency requirements is a complex endeavor, and it's crucial to plan and implement your data localization strategy carefully. Additionally, consider working with professionals who specialize in data privacy and compliance to ensure that your app remains in compliance with evolving regulations.